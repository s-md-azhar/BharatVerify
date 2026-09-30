import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { NewVerification } from './pages/NewVerification';
import { AuditTrail } from './pages/AuditTrail';
import { Evaluation } from './pages/Evaluation';
import { CaseDetails } from './pages/CaseDetails';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="verify" element={<NewVerification />} />
          <Route path="audit" element={<AuditTrail />} />
          <Route path="eval" element={<Evaluation />} />
          <Route path="cases/:id" element={<CaseDetails />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
