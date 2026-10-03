from tools.rag_tools import retrieve_knowledge


results = retrieve_knowledge(
    "What should a patient bring to an appointment?"
)

print("RAG RESULTS")
print("=" * 50)

for result in results:

    print(result)
    print("=" * 50)
