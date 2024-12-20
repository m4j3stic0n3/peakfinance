import React from 'react';
    import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
    import HomeScreen from './screens/HomeScreen';
    import QuizScreen from './screens/QuizScreen';
    import PortfolioScreen from './screens/PortfolioScreen';
    import AIAssistantScreen from './screens/AIAssistantScreen';
    import LearningScreen from './screens/LearningScreen';
    import Sidebar from './components/Sidebar';
    import './App.css';

    function App() {
      return (
        <Router>
          <div className="app-container">
            <Sidebar />
            <div className="content">
              <Routes>
                <Route path="/" element={<HomeScreen />} />
                <Route path="/quiz" element={<QuizScreen />} />
                <Route path="/portfolio" element={<PortfolioScreen />} />
                <Route path="/ai-assistant" element={<AIAssistantScreen />} />
                <Route path="/learning" element={<LearningScreen />} />
              </Routes>
            </div>
          </div>
        </Router>
      );
    }

    export default App;
