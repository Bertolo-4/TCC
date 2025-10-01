# TODO: Integrate ChatGPT API for Exercise Explanation

- [x] Install OpenAI Python client library
- [x] Add new Pydantic models in models.py: ExerciseExplainRequest and ExerciseExplainResponse
- [x] Create openai_client.py for OpenAI integration logic
- [x] Add new POST endpoint /explain-exercise in routes.py
- [x] Set up OPENAI_API_KEY environment variable (User needs to set OPENAI_API_KEY in environment)
- [x] Test the new endpoint (Requires OPENAI_API_KEY set; run server with uvicorn main:app --reload and POST to /explain-exercise)
