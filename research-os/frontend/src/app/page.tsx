'use client';

import { useEffect, useRef, useState } from "react";

export default function Home() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [papers, setPapers] = useState<any[]>([]);
  const [selectedPaper, setSelectedPaper] = useState<any>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  useEffect(() => {
    const loadPapers = async() => {
      const res = await fetch("http://localhost:8000/papers");
      const data = await res.json();
      setPapers(data);
      
      if(data.length>0){
        setSelectedPaper(data[data.length-1]);
      }
    };
    loadPapers();
  }, []);

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  }

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>)=>{
    const file = e.target.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });
    const papersRes = await fetch("http://localhost:8000/papers");
    const papersData = await papersRes.json();
    setPapers(papersData);
    if(papersData.length>0){
      setSelectedPaper(papersData[papersData.length-1]);
    };
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">ResearchOS</h1>
          <button onClick={handleUploadClick} className="bg-black text-white px-4 py-2 rounded-lg">
            Upload Paper
          </button>


          <input
            type="file"
            accept="application/pdf"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
          />
        </div>

        {selectedPaper && (
          <div className="mb-6 bg-white rounded-xl shadow p-6">
            <h2 className="text-2xl font-bold mb-2">
              {selectedPaper.title}
            </h2>
            <p className="text-gray-600 mb-6">
              {selectedPaper.summary}
            </p>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold">Objective</h3>
                <p>{selectedPaper.objective}</p>
              </div>
              <div>
                <h3 className="font-semibold">Methods</h3>
                <p>{selectedPaper.methods}</p>
              </div>
              <div>
                <h3 className="font-semibold">Dataset</h3>
                <p>{selectedPaper.dataset}</p>
              </div>
              <div>
                <h3 className="font-semibold">Research Gap</h3>
                <p>{selectedPaper.research_gap}</p>
              </div>

              <div>
                <h3 className="font-semibold mb-2">Keywords</h3>
                <div className="flex flex-wrap gap-2">
                  {String(selectedPaper.keywords)
                    .replace("[", "")
                    .replace("]", "")
                    .replaceAll("'", "")
                    .split(",")
                    .map((keyword: string, index: number) => (
                      <span
                        key={index}
                        className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm"
                      >
                        {keyword.trim()}
                      </span>
                    ))
                  }
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-3 gap-4">
          
          <div className="col-span-1 bg-white p-4 rounded-xl shadow">
            <h2 className="font-semibold mb-2">Your Papers</h2>
            {papers.length === 0 ? (
              <p className="text-gray-500">No papers uploaded yet.</p>
            ) : (
              <div className="space-y-3">
                  {papers.map((paper) => (
                    <div
                      key={paper.id}
                      onClick={()=>setSelectedPaper(paper)}
                      className="border rounded-lg p-3 hover:bg-gray-50 cursor-pointer"
                    >
                        <h3 className="font-medium text-sm">{paper.title}</h3>
                        <p className="text-xs text-gray-500 mt-1">{paper.doi}</p>
                    </div>
                  ))}
              </div>
            )}
          </div>

          <div className="col-span-2 bg-white p-4 rounded-xl shadow">
            <h2 className="font-semibold mb-2">Knowledge Graph</h2>
            <div className="h-64 flex items-center justify-center text-gray-400">
              Graph will appear here
            </div>
          </div>
      
      </div>      

      <div className="mt-4 bg-white p-4 rounded-xl shadow">
        <h2 className="font-semibold mb-2">AI Research Assistant</h2>        
        <div className="space-y-3">
          <textarea
            value={question}
            onChange={(e)=>setQuestion(e.target.value)}
            placeholder="Ask anything about your research..."
            className="w-full border rounded-lg p-3"
          />
          <button
            className="bg-black text-white px-4 py-2 rounded-lg"
          >
            Ask AI
          </button>
          {answer && (
            <div className="bg-gray-100 rounded-lg p-4">
              {answer}
            </div>
          )}
        </div>
      </div>
    </div>
  </div>
  );
}