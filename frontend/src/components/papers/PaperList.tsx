import PaperCard from "./PaperCard";
import { EmptyState } from "../common/EmptyState";
import type { PaperListItem } from "../../types/paper";

interface PaperListProps {
  papers: readonly PaperListItem[];
  onPaperClick?: (paperId: number) => void;
}

function PaperList({
  papers,
  onPaperClick,
}: Readonly<PaperListProps>) {
  if (papers.length === 0) {
    return (
      <EmptyState
        title="No papers found"
        message="Try changing your search criteria or filters."
      />
    );
  }

  return (
    <section
      className="paper-list"
      aria-label="Research papers"
    >
      {papers.map((paper) => (
        <PaperCard
          key={paper.paper_id}
          paper={paper}
          onClick={onPaperClick}
        />
      ))}
    </section>
  );
}

export default PaperList;