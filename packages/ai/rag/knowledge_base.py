"""Minimal in-memory knowledge base for local waste rules. Each document
carries source metadata. This is a keyword-matching retriever — swap for a
real embedding index (packages/ai/rag/embeddings.py) once a vector store is
wired up; the retriever interface stays the same."""

DOCUMENTS = [
    {
        "id": "rule-plastic-1",
        "title": "PET plastic recycling guidance",
        "jurisdiction": "default",
        "text": "PET plastic bottles should be rinsed and have caps removed before "
                 "placing in the dry recyclable bin. Contaminated PET with food residue "
                 "is not accepted by most municipal recycling streams.",
    },
    {
        "id": "rule-ewaste-1",
        "title": "E-waste handling guidance",
        "jurisdiction": "default",
        "text": "Electronic waste must never be placed in general waste bins. It should be "
                 "taken to an authorized e-waste collection point due to hazardous components "
                 "such as batteries and circuit boards.",
    },
    {
        "id": "rule-medical-1",
        "title": "Medical waste compliance",
        "jurisdiction": "default",
        "text": "Sharps, infectious and pharmaceutical waste require licensed facility "
                 "handling and cannot be processed through standard municipal collection.",
    },
    {
        "id": "rule-organic-1",
        "title": "Organic and food waste guidance",
        "jurisdiction": "default",
        "text": "Fresh, unspoiled surplus food within a safe holding window is eligible "
                 "for donation. Spoiled food or food past the safe holding window should "
                 "be composted rather than donated.",
    },
]
