from datetime import datetime
from database.vector_store import VectorStore
from services.synthesizer import Synthesizer
from timescale_vector import client

# Initialize VectorStore
vec = VectorStore()

relevant_question = "Passionate Backend Developer with expertise in building robust and efficient server-side applications. Proficient in programming languages such as Python, Java, and Go, with experience in frameworks such as Flask, Spring Boot, and Gin. Skilled in designing and optimizing database schemas, implementing caching mechanisms, and optimizing application performance. Led projects such as developing real-time messaging systems, building RESTful APIs for fintech platforms, and integrating payment gateways. Also contributed to projects including implementing message queues for asynchronous processing, designing and implementing database migrations, and ensuring application security through encryption and data masking techniques. Actively participating in backend development communities and forums to share knowledge and collaborate with peers."
results = vec.search(relevant_question, limit=3)

response = Synthesizer.generate_response(question=relevant_question, context=results)

print(f"\n{response.answer}")
print("\nThought process:")
for thought in response.thought_process:
    print(f"- {thought}")
print(f"\nContext: {response.enough_context}")

# --------------------------------------------------------------
# Irrelevant question
# --------------------------------------------------------------

irrelevant_question = "What is the weather in Tokyo?"

results = vec.search(irrelevant_question, limit=3)

response = Synthesizer.generate_response(question=irrelevant_question, context=results)

print(f"\n{response.answer}")
print("\nThought process:")
for thought in response.thought_process:
    print(f"- {thought}")
print(f"\nContext: {response.enough_context}")

metadata_filter = {"category": "Job description"}

results = vec.search(relevant_question, limit=3, metadata_filter=metadata_filter)

response = Synthesizer.generate_response(question=relevant_question, context=results)

print(f"\n{response.answer}")
print("\nThought process:")
for thought in response.thought_process:
    print(f"- {thought}")
print(f"\nContext: {response.enough_context}")

# --------------------------------------------------------------
# Advanced filtering using Predicates
# --------------------------------------------------------------

predicates = client.Predicates("category", "==", "Job description")
results = vec.search(relevant_question, limit=3, predicates=predicates)


predicates = client.Predicates("category", "==", "Job description") | client.Predicates(
    "category", "==", "Services"
)
results = vec.search(relevant_question, limit=3, predicates=predicates)


predicates = client.Predicates("category", "==", "Job description") & client.Predicates(
    "created_at", ">", "2024-09-01"
)
results = vec.search(relevant_question, limit=3, predicates=predicates)

# --------------------------------------------------------------
# Time-based filtering
# --------------------------------------------------------------

# September — Returning results
time_range = (datetime(2024, 9, 1), datetime(2024, 9, 30))
results = vec.search(relevant_question, limit=3, time_range=time_range)

# August — Not returning any results
time_range = (datetime(2024, 8, 1), datetime(2024, 8, 30))
results = vec.search(relevant_question, limit=3, time_range=time_range)
