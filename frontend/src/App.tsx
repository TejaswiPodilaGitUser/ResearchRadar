import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import MainNavigation from "./components/navigation/MainNavigation";

import HomePage from "./pages/HomePage";
import SearchPage from "./pages/SearchPage";
import AuthorsPage from "./pages/AuthorsPage";
import TopicsPage from "./pages/TopicsPage";
import TopicDetailPage from "./pages/TopicDetailPage";
import RecommendationsPage from "./pages/RecommendationsPage";
import PaperDetailPage from "./pages/PaperDetailPage";
import Metrics from "./pages/Metrics";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <div className="app">

        <MainNavigation />

        <Routes>

          <Route
            path="/"
            element={<HomePage />}
          />

          <Route
            path="/papers"
            element={<SearchPage />}
          />

          <Route
            path="/papers/:paperId"
            element={<PaperDetailPage />}
          />

          <Route
            path="/authors"
            element={<AuthorsPage />}
          />

          <Route
            path="/topics"
            element={<TopicsPage />}
          />

          <Route
            path="/topics/:topicId"
            element={<TopicDetailPage />}
          />

          <Route
            path="/recommendations"
            element={<RecommendationsPage />}
          />

          <Route
            path="/metrics"
            element={<Metrics />}
          />

          <Route
            path="*"
            element={
              <Navigate
                to="/"
                replace
              />
            }
          />

        </Routes>

      </div>
    </BrowserRouter>
  );
}

export default App;

