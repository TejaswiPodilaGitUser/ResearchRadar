import type { PaperListItem } from "../../types/paper";

interface PaperCardProps {
  paper: PaperListItem;
  onClick?: (paperId: number) => void;
}

function PaperCard({
  paper,
  onClick,
}: Readonly<PaperCardProps>) {
  const handleClick = () => {
    onClick?.(paper.paper_id);
  };

  return (
    <article className="paper-card">
      <h3 className="paper-title">
        {paper.paper_name}
      </h3>

      <div className="paper-meta">
        {paper.publication_year !== null &&
          paper.publication_year !== undefined && (
            <span>
              Published: {paper.publication_year}
            </span>
          )}

        {paper.cited_by_count !== null &&
          paper.cited_by_count !== undefined && (
            <span className="citation-badge">
              Citations: {paper.cited_by_count}
            </span>
          )}
      </div>

      {paper.abstract && (
        <p className="paper-abstract">
          {paper.abstract}
        </p>
      )}

      {onClick !== undefined && (
        <button
          type="button"
          className="paper-action"
          onClick={handleClick}
        >
          View Paper
        </button>
      )}
    </article>
  );
}

export default PaperCard;