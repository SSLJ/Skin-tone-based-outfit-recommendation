import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";
import AnalyzePage from "./pages/AnalyzePage/AnalyzePage";
import ResultsPage from "./pages/ResultsPage/ResultsPage";

export default function App() {
  const [result, setResult] = useState(null);
  const [inputMethod, setInputMethod] = useState(null); // "image" | "manual"

  function handleResult(data, method) {
    setResult(data);
    setInputMethod(method);
  }

  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<AnalyzePage onResult={handleResult} />} />
        <Route
          path="/results"
          element={<ResultsPage result={result} inputMethod={inputMethod} />}
        />
      </Routes>
    </BrowserRouter>
  );
}
