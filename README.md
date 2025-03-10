# AI-Powered Student Progress Report Generator

## Overview

The AI-Powered Student Progress Report Generator is a Flask-based web application designed to generate AI-driven student progress reports. By leveraging Google Gemini AI, MongoDB, and ReportLab, the system analyzes milestone data and provides personalized progress summaries along with recommendations. The generated reports are available for download in PDF format.

## Aim

- The key objectives of this project are:

- Data Collection: Store and retrieve student milestones from MongoDB.

- AI-Powered Report Generation: Use Google Gemini API to create insightful progress reports.

- PDF Generation: Format and export reports as PDF files using ReportLab.

- Interactive Web Interface: Provide a user-friendly UI to input data and generate reports.

## Technologies Used

- Frontend: HTML, CSS, JavaScript

- Backend: Flask, Python

- Database: MongoDB (via pymongo)

- AI Model: Google Gemini API (gemini-1.5-pro)

- PDF Generation: ReportLab

## How It Works

1. User Inputs Student Information:

   - Name
   - Age
   - Developmental milestones
   - Other details

2. Data Retrieval from MongoDB:

   - The system fetches the relevant milestone data based on the student’s age.

3. AI-Generated Progress Summary:

   - Google Gemini API processes the data to create a personalized progress evaluation.

4. PDF Report Generation:

   - ReportLab formats the AI-generated insights into a structured PDF document.
   - The report is available for download after generation.

## Database Structure

The MongoDB database contains records of student developmental milestones. Each entry consists of:

- DevelopmentalArea (e.g., Cognitive-Development, Motor Skills, Social-Emotional Development)

- Age (Integer: represents the age of the student)

- Milestone (String: describes the developmental achievement)

- Definition (String: explanation of the milestone)

- Intervention (String: suggested activities to improve the skill)

## Usage

1. Enter Student Details

   - Provide the student’s name and age.
   - Select the relevant developmental milestones.

2. Generate Report

   - Click the Generate Report button.
   - The AI processes the data and formats a PDF file.

3. Download the Report

   - Once generated, the PDF is available for download.

## Features

- AI-Powered Insights - Generates student progress reports using Google Gemini API.

- MongoDB Integration - Retrieves milestone data dynamically.

- PDF Export - Generates structured progress reports in PDF format.

- User-Friendly UI - Simple and interactive design for easy navigation.

- Real-time Feedback - AI-generated recommendations to enhance student growth.

## API Endpoints

| **Method** | **Endpoint**       | **Description**                        |
| ---------- | ------------------ | -------------------------------------- |
| `GET`      | `/`                | Render Homepage                        |
| `GET`      | `/get_milestones`  | Retrieves milestones from the database |
| `POST`     | `/generate_report` | Process input & return PDF report      |

## Dependencies

The following packages are required and included in `requirements.txt`:

```bash
flask
pymongo
google-generativeai
reportlab
python-dotenv
```

## Installation & Setup

### Prerequisites

Ensure you have `Python 3.8+` installed on your system.

### Steps

1. Clone the Repository:

   ```bash
   git clone https://github.com/PriyanshuLathi/AI-Powered-Student-Progress-Report-Generator.git
   cd AI-Powered-Student-Progress-Report-Generator
   ```

2. Create and Activate a Virtual Environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install Dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set Up Environment Variables:

   - Create a `.env` file in the root directory.

   - Add the following variables:

   ```bash
   MONGO_URL=<your_mongo_db_connection_string>
   GEMINI_API_KEY=<your_google_gemini_api_key>
   ```

5. Run the Application:

   ```bash
   python app.py
   ```

6. Access the app in your browser at `http://127.0.0.1:5000`.

## Future Enhancements

- Multilingual Support: Provide reports in different languages.

- Email Reports: Automatically send reports via email.

- Dashboard Analytics: Track student progress over time.

## Contribution Guidelines

Contributions are Welcome! To contribute:

1. Fork the repository.

2. Create a new branch:

   ```bash
   git checkout -b feature-branch-name
   ```

3. Make your changes and commit:

   ```bash
   git commit -m "Added new feature"
   ```

4. Push to your fork:

   ```bash
   git push origin feature-branch-name
   ```

5. Open a Pull Request for review.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/PriyanshuLathi/AI-Powered-Student-Progress-Report-Generator/blob/main/LICENSE) file for details.

## Contact

For any questions or feedback:

- **LinkedIn**: [Priyanshu Lathi](https://www.linkedin.com/in/priyanshu-lathi)
- **GitHub**: [Priyanshu Lathi](https://github.com/PriyanshuLathi)

## Authors

- **Priyanshu Lathi**
