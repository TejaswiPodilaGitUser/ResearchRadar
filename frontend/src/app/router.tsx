import {
  createBrowserRouter,
  Navigate,
} from "react-router-dom";

import SearchPage from "../pages/SearchPage";
import PaperDetailPage from "../pages/PaperDetailPage";

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
]);