from together import Together
import os

# Configure Together API
os.environ["TOGETHER_API_KEY"] = "4fd820781ff0ffeb5ffa6292b298da0e893fccdc0a14755374f6cd99cc95ebd6"  # Replace with your actual API key
api_client = Together()

# def analyze_pdf(pdf_text, job_description):
#     """
#     Analyze the PDF content based on the job description using Together API.

#     Args:
#         pdf_text (str): Extracted text from the PDF.
#         job_description (str): Job description text provided by the user.

#     Returns:
#         dict: A dictionary containing scores, strengths, weaknesses, and fit analysis.
#     """
#     try:
#         user_input = f"Job Description: {job_description}\nResume Text: {pdf_text}"
        
#         # Make API request
#         api_response = api_client.chat.completions.create(
#             model="meta-llama/Llama-Vision-Free",
#             messages=[{"role": "user", "content": user_input}]
#         )

#         # Parse the response
#         result_content = api_response.choices[0].message.content.strip()
        
#         # Extract strengths, weaknesses, and fit from the result
#         # This assumes the API provides data in a structured manner. Adjust parsing as needed.
#         return {
#             "analysis": result_content
#         }

#     except Exception as e:
#         print(f"Error during API call: {e}")
#         return {"error": str(e)}
def analyze_pdf(pdf_text, job_description):
    """
    Analyze the PDF content based on the job description using Together API.

    Args:
        pdf_text (str): Extracted text from the PDF.
        job_description (str): Job description text provided by the user.

    Returns:
        dict: A dictionary containing analysis results, including candidate name.
    """
    try:
        user_input = f"""Job Description: {job_description}\nResume Text: {pdf_text}
        # Role and Purpose
    You are an AI assistant designed to evaluate resumes against specific parameters such as job descriptions, required skills, and experience. 
    Your task is to generate a detailed, structured report indicating whether the resume is suitable for the given job description and provide a 
    score and reasoning.

    # Guidelines:
    1. Assess the resume based on the job description, required skills, experience, and other provided parameters.
    2. Clearly state whether the resume meets the criteria and why.
    3. Provide a suitability score between 0 and 100, where:
        - 0-40: Poor fit
        - 41-70: Moderate fit
        - 71-100: Excellent fit
    4. Highlight key strengths of the resume and areas for improvement.
    5. Maintain a professional and constructive tone, offering actionable feedback to the candidate.
    6. If there is insufficient information to fully evaluate the resume, state this explicitly and suggest what is missing.
    7. Adhere to the following structured format for the response:

    ---
    **Suitability Report:**
    - Suitability Score: [Score] out of 100
    - Verdict: [Good Fit / Moderate Fit / Poor Fit]

    **Strengths:**
    - [List key strengths of the resume in bullet points]

    **Areas for Improvement:**
    - [List specific weaknesses or missing elements in bullet points]

    **Reasoning:**
    - Provide a detailed explanation for the score, referencing specific aspects of the resume and job description.

    **Additional Information (if needed):**
    - Mention any missing details or additional context required for a complete evaluation.
    ---

    # Example Scenarios:
    - If the resume lacks critical skills mentioned in the job description, highlight the gap and explain how it impacts suitability.
    - If the resume has strong qualifications but is missing industry-specific experience, provide suggestions to improve it.

    Carefully review the job description, resume details, and any other context before generating the report.
    """
        
        # Make API request
        api_response = api_client.chat.completions.create(
            model="meta-llama/Llama-Vision-Free",
            messages=[{"role": "user", "content": user_input}]
        )

        # Extract the response content
        result_content = api_response.choices[0].message.content.strip()

        # Placeholder logic to extract candidate name (modify based on response structure)
        candidate_name = "Unknown Candidate"  # Update with actual logic if API returns a name

        return {
            "candidate_name": candidate_name,
            "analysis": result_content,
        }

    except Exception as e:
        print(f"Error during API call: {e}")
        return {"error": str(e)}
