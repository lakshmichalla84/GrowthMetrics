from flask import Flask, render_template, request, send_file, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from ai_setup import process_observation
import io
import json
import sys
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import re

load_dotenv()

app = Flask(__name__)

# MongoDB setup
try:
    MONGO_URL = os.getenv("MONGO_URL")
    if not MONGO_URL:
        raise ValueError("MongoDB URL is missing!")
    client = MongoClient(MONGO_URL)
    db = client['report_generator']
    collection = db['milestones']
except Exception as e:
    print("MongoDB Connection Error:", str(e))
    sys.exit(1)  # Exit if connection fails


def generate_pdf(student_data, ai_summaries, activity_recommendations):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []

    story.append(Image('SpacECE.jpg', 1.4*inch, 1.4*inch))
    story.append(Spacer(1, 20))


    story.append(Paragraph("STUDENT PROGRESS REPORT", styles['Title']))
    story.append(Spacer(1, 12))

    basic_info_fields = [
        ('Child\'s Name', 'name'),
        ('Age', 'age'),
        ('Date of Birth', 'dob'), 
        ('Class', 'class'), 
        ('Date of Assessment', 'doa'), 
        ('Assessor\'s Name', 'assessor'), 
    ]

    for field, form_key in basic_info_fields:
        story.append(Paragraph(f"{field}: {student_data.get(form_key, 'N/A')}", styles['Normal']))
        story.append(Spacer(1, 12))

    env_map = {
        '0': 'Home',
        '1': 'Daycare',
        '2': 'Other'
    }

    env = env_map.get(student_data.get('env', 'N/A'), 'N/A')
    story.append(Paragraph(f"Environment: {env}", styles['Normal']))
    story.append(Spacer(1, 12))

    development_areas = list(ai_summaries.keys())

    for i, area in enumerate(development_areas, 1):
        story.append(Paragraph(f"{i}. {area}", styles['Heading2']))
        story.append(Paragraph(f"{ai_summaries.get(area, 'No summary generated')}", styles['Normal']))
        story.append(Spacer(1, 8))

    delay_map = {
        '0': 'On track',
        '1': 'Slight Delay',
        '2': 'Significant Delay'
    }

    progress = delay_map.get(student_data.get('delay', 'N/A'), 'N/A')
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"Overall Development Progress: {progress}", styles['Heading2']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Recommendations/Next Steps", styles['Heading2']))
    story.append(Paragraph("Activities/Therapies recommended:", styles['Normal']))
    story.append(Spacer(1, 6))

    recommendations_list = activity_recommendations.strip().split('\n')
    for rec in recommendations_list:
        rec_cleaned = rec.lstrip('*').strip()
        story.append(Paragraph(f"• {rec_cleaned}", styles['Normal']))

    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Next Assessment Date: {student_data.get('next_date', 'N/A')}", styles['Heading2']))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Assessor's Signature: ___________________", styles['Heading2']))
    story.append(Spacer(1, 4))

    story.append(Paragraph(f"Parent's signature: ______________________", styles['Heading2']))

    doc.build(story)
    buffer.seek(0)
    return buffer


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_milestones', methods=['GET'])
def get_milestones():
    age = request.args.get('age')

    if not age:
        return jsonify({"error": "Age is required"}), 400

    try:
        if '.' in age:
            age = float(age)
        else:
            age = int(age)

        milestones = list(collection.find(
            {"Age": int(age)}, {"_id": 0, "DevelopmentalArea": 1, "Milestone": 1}
        ))

        # Grouped milestones by DevelopmentalArea
        grouped_milestones = {}
        for milestone in milestones:
            area = milestone["DevelopmentalArea"]
            if area not in grouped_milestones:
                grouped_milestones[area] = []
            grouped_milestones[area].append(milestone["Milestone"])

        return jsonify({"milestones": grouped_milestones})

    except ValueError:
        return jsonify({"error": "Invalid age format"}), 400


@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        student_data = request.form.to_dict()
        name = student_data.get('name', '')
        age = student_data.get('age', '')
        class_name = student_data.get('class', '')
        delay = student_data.get('delay', '')

        # Fetching all milestones for the given age from MongoDB
        milestones = list(collection.find(
            {"Age": int(age)}, {"_id": 0, "DevelopmentalArea": 1, "Milestone": 1}
        ))

        # Creating a mapping: { "Milestone Name" -> "Developmental Area" }
        milestone_mapping = {m["Milestone"]: m["DevelopmentalArea"] for m in milestones}

        milestone_data = {}

        for key, value in request.form.items():
            if key.startswith("milestone_"):
                milestone_name = key.replace("milestone_", "").replace("_", " ")
                developmental_area = milestone_mapping.get(milestone_name, "Unknown")  # Get area from DB
                
                if developmental_area not in milestone_data:
                    milestone_data[developmental_area] = {}
                milestone_data[developmental_area][milestone_name] = int(value)

        # print(milestone_data)

        if not milestone_data:
            return jsonify({"error": "No milestones selected"}), 400

        milestone_json = json.dumps(milestone_data, indent=2)
        # print(milestone_json)

        # Now, passing structured JSON to Gemini API
        prompt = f"""You are an expert assessor who evaluates children's developmental progress at SpacECE India Foundation.

        Child's Name: {name}
        Age: {age}
        Class: {class_name}
        
        Below are {name}'s assessment results:

        {milestone_json}

        ### Guidelines for Report Generation:
        1. Provide a **separate progress summary** for each developmental area.
        2. **Start with an overall progress statement** for each area.
        3. **Mention 1-2 strongest skills** (scores of 3).
        4. **Highlight 1-2 skills needing improvement** (scores of 1) and clearly explain why improvement is needed.
        5. **If a child scores mostly 1s**, emphasize that **significant support and intervention** are required.
        6. Use **simple and clear language** so parents can easily understand.
        7. Keep each section **concise (50-75 words per area)**.
        8. Maintain an **encouraging tone**, but do not avoid mentioning challenges when they exist.

        ### Score Interpretation:
        - **1**: Needs Significant Improvement (Struggles in this area, requires extra attention and structured activities).
        - **2**: Developing as Expected (Moderate progress, could use more practice).
        - **3**: Excelling in This Area (Strong ability, demonstrates mastery).

        ### Expected Format (Don't make the sentence repetitive, it should seem natural):
        **Developmental Area:**
        "{name} is making [adjective] progress in the development area. They excel at [Skill1] and [Skill2], etc. We recommend additional practice with [Skill3] to [benefit], etc." or "{name} is currently facing challenges in [Developmental Area]. They struggle with [Skill1] and [Skill2], making it difficult to [explain impact]. Focused activities such as [specific recommendation] can help them improve. Continued support is needed."

        **Now, generate the full report based on this data:**
        """

        # Gemini API call
        response = process_observation(prompt)

        if 'content' not in response:
            return jsonify({"error": "AI response error"}), 500

        full_text = response['content']
        ai_summaries = {match[0].strip(): match[1].strip() for match in re.findall(r"\*\*(.*?)\*\*\n\n(.*?)(?=\n\n\*\*|\Z)", full_text, re.DOTALL)}

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    recommendations_prompt = f"""Generate 3-5 development recommendations for {name} ({age} years old) based on these assessments:

    {milestone_json}
    
    Progress Level: {delay}

    Guidelines:
    - Focus on lowest scoring areas (scores=1)
    - Include both home and school activities
    - Suggest concrete, age-appropriate exercises
    - Format as bullet points using simple language
    - Max 1 sentence per recommendation
    - Keep it free from placeholders or bullets or symbols like * or -, give plain text

    Example:
    - Practice throwing/catching soft balls daily
    - Encourage crayon scribbling with both hands

    Actual Recommendations:
    """

    try:
        recommendations = process_observation(recommendations_prompt)['content']
    except Exception as e:
        recommendations = f"Recommendations unavailable: {str(e)}"

    pdf_buffer = generate_pdf(student_data, ai_summaries, recommendations)
    
    return send_file(
        pdf_buffer, 
        download_name=f'{name}_progress_report.pdf',
        mimetype='application/pdf',
        as_attachment=True
    )


if __name__ == '__main__':
    app.run()
