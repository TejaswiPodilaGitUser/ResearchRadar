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

      {paper.authors && paper.authors.length > 0 && (
        <p className="paper-authors">
          Authors:{" "}
          {paper.authors
            .map((author) => author.author_name)
            .join(", ")}
        </p>
      )}

      <div className="paper-meta">
        <span>
          Paper ID: {paper.paper_id}
        </span>

        {paper.publication_year !== null &&
          paper.publication_year !== undefined && (
            <span>
              Published: {paper.publication_year}
            </span>
          )}

        {paper.cited_by_count !== null &&
          paper.cited_by_count !== undefined && (
            <span>
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