import {
  createBrowserRouter,
  Navigate,
} from "react-router-dom";

import SearchPage from "../pages/SearchPage";
import PaperDetailPage from "../pages/PaperDetailPage";
import Metrics from "../pages/Metrics";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/search" replace />,
  },
  {
    path: "/search",
    element: <SearchPage />,
  },
  {
    path: "/papers/:paperId",
    element: <PaperDetailPage />,
  },
  {
    path: "/metrics",
    element: <Metrics />,
  },
]);