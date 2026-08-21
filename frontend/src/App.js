import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { NotificationProvider } from "./context/NotificationContext";
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";
import RecoveryRequest from "./components/auth/RecoveryRequest";
import ResetCredentials from "./components/auth/ResetCredentials";
import AdminDashboard from "./components/admin/AdminDashboard";
import CharactersHub from "./components/CharactersHub";
import CharacterSheet from "./components/CharacterSheet";
import CharacterForm from "./components/CharacterForm";
import UserProfile from "./components/profile/UserProfile";
import LandingPage from "./components/LandingPage";
import RunGenerator from "./components/RunGenerator";
import SavedRuns from "./components/SavedRuns";
import HostHub from "./components/hosting/HostHub";
import HostedRunPage from "./components/hosting/HostedRunPage";
import SocialBar from "./components/layout/SocialBar";
import ReportPage from "./components/ReportPage";
import InformationPage from "./components/InformationPage";
import NotificationPoller from "./components/NotificationPoller";
import "./App.css";
import "./styles/theme.css";
import "./styles/SocialBar.css";

const ProtectedRoute = ({ children }) => {
    const { token, loading } = useAuth();
    
    if (loading) return <div style={{ color: "white", padding: "50px", textAlign: "center" }}>Checking authentication...</div>;
    
    if (!token) {
        return <Navigate to="/login" replace />;
    }
    
    return children;
};

const AdminProtectedRoute = ({ children }) => {
    const { token, user, loading } = useAuth();
    
    if (loading) return <div style={{ color: "white", padding: "50px", textAlign: "center" }}>Checking authorization...</div>;
    
    if (!token || !user?.is_admin) {
        return <Navigate to="/" replace />;
    }
    
    return children;
};

function App() {
  return (
    <AuthProvider>
      <NotificationProvider>
        <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <NotificationPoller />
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/run-generator" element={<RunGenerator />} />
            <Route path="/informations" element={<InformationPage />} />
            <Route path="/saved-runs" element={<ProtectedRoute><SavedRuns /></ProtectedRoute>} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/recovery-request" element={<RecoveryRequest />} />
            <Route path="/reset-credentials" element={<ResetCredentials />} />
            <Route path="/admin" element={<AdminProtectedRoute><AdminDashboard /></AdminProtectedRoute>} />
            <Route path="/profile/:id" element={<ProtectedRoute><UserProfile /></ProtectedRoute>} />
            <Route path="/hosting" element={<ProtectedRoute><HostHub /></ProtectedRoute>} />
            <Route path="/hosting/:id" element={<ProtectedRoute><HostedRunPage /></ProtectedRoute>} />
            <Route path="/characters" element={<ProtectedRoute><CharactersHub /></ProtectedRoute>} />
            <Route path="/characters/:id" element={<ProtectedRoute><CharacterSheet /></ProtectedRoute>} />
            <Route path="/characters/create" element={<ProtectedRoute><CharacterForm /></ProtectedRoute>} />
            <Route path="/characters/:id/edit" element={<ProtectedRoute><CharacterSheet /></ProtectedRoute>} />
            <Route path="/report" element={<ProtectedRoute><ReportPage /></ProtectedRoute>} />
          </Routes>
          <SocialBar />
        </BrowserRouter>
      </NotificationProvider>
    </AuthProvider>
  );
}

export default App;