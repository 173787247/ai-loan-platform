import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { UserProvider } from './contexts/UserContext';
import { NotificationProvider } from './components/NotificationSystem';
import UserNavbar from './components/UserNavbar';
import AIChatbot from './components/AIChatbot';
import Home from './pages/Home';
import Login from './pages/Login';
import RiskAssessment from './pages/RiskAssessment';
import AutoMatching from './pages/AutoMatching';
import RealtimeMonitoring from './pages/RealtimeMonitoring';
import AIChatbotDemo from './pages/AIChatbotDemo';
import NotificationDemo from './pages/NotificationDemo';
import Notifications from './pages/Notifications';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import Reports from './pages/Reports';
import AIEnhancements from './pages/AIEnhancements';
import Workflow from './pages/Workflow';
import Integrations from './pages/Integrations';
import Microservices from './pages/Microservices';
import RiskManagement from './pages/RiskManagement';
import Compliance from './pages/Compliance';
import './App.css';

function App() {
  return (
    <UserProvider>
      <NotificationProvider>
        <Router>
          <div className="App">
            <UserNavbar />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/risk-assessment" element={<RiskAssessment />} />
              <Route path="/auto-matching" element={<AutoMatching />} />
              <Route path="/realtime-monitoring" element={<RealtimeMonitoring />} />
              <Route path="/ai-chatbot-demo" element={<AIChatbotDemo />} />
              <Route path="/notification-demo" element={<NotificationDemo />} />
              <Route path="/notifications" element={<Notifications />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/ai-enhancements" element={<AIEnhancements />} />
              <Route path="/workflow" element={<Workflow />} />
              <Route path="/integrations" element={<Integrations />} />
              <Route path="/microservices" element={<Microservices />} />
              <Route path="/risk-management" element={<RiskManagement />} />
              <Route path="/compliance" element={<Compliance />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
            <AIChatbot />
          </div>
        </Router>
      </NotificationProvider>
    </UserProvider>
  );
}

export default App;