# Research Summarizer
Overall idea (this is big project i might be shooting a little too high)

1. Upload papers
2. extract all text
3. get ai to get information from each paper and put it into a json
- paperid, title, authors, year, journal, doi, url, research domain, keywords, research question, objective, hypothesis, methods, moels used, datasets, dataset public, dataset links, sample size, variables, main results, conclusion, limitations, research gap, future work, applications, related topics, interesting quotes, my notes, confidence score, connections, paragraph summary
(process paper in background after the user uploads it)
4. graph agent, finds conneections to every paper and adds the "connections" to json
5. database agent saves everything safely
6. chat agent answers questions abt papers


# Architcture:
frontend - react & next.js
styling - tailwind css
backend api - fastapi (python)
AI - hack club ai
file storage-  local (maybe change later)
knowledge graph - sqlite