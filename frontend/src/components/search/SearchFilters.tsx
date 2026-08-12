interface SearchFiltersProps {
  year?: number;
  topic?: string;
  author?: string;
  years: readonly number[];
  onYearChange: (year?: number) => void;
  onTopicChange: (topic: string) => void;
  onAuthorChange: (author: string) => void;
  onClear: () => void;
}

function SearchFilters({
  year,
  topic = "",
  author = "",
  years,
  onYearChange,
  onTopicChange,
  onAuthorChange,
  onClear,
}: Readonly<SearchFiltersProps>) {
  return (
    <>
      <div className="filters">
        <div className="filter">
          <label htmlFor="year-filter">
            Publication Year
          </label>

          <select
            id="year-filter"
            value={year ?? ""}
            onChange={(event) => {
              const value = event.target.value;

              onYearChange(
                value === ""
                  ? undefined
                  : Number(value),
              );
            }}
          >
            <option value="">
              All years
            </option>

            {years.map((availableYear) => (
              <option
                key={availableYear}
                value={availableYear}
              >
                {availableYear}
              </option>
            ))}
          </select>
        </div>

        <div className="filter">
          <label htmlFor="topic-filter">
            Topic
          </label>

          <input
            id="topic-filter"
            type="text"
            value={topic}
            onChange={(event) =>
              onTopicChange(event.target.value)
            }
            placeholder="Filter by topic"
          />
        </div>

        <div className="filter">
          <label htmlFor="author-filter">
            Author
          </label>

          <input
            id="author-filter"
            type="text"
            value={author}
            onChange={(event) =>
              onAuthorChange(event.target.value)
            }
            placeholder="Filter by author"
          />
        </div>
      </div>

      <button
        type="button"
        className="clear-filters"
        onClick={onClear}
      >
        Clear Filters
      </button>
    </>
  );
}

export default SearchFilters;