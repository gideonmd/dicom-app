import { Routes, Route, Outlet, Link } from "react-router-dom";
import Directory from './pages/Directory';
import DicomImage from './pages/DicomImage';

export default function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Directory />} />
        <Route path="/image/:id" element={<DicomImage />} />
      </Routes>
    </div >
  )
}
