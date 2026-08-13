import {
  SEARCH_MODE_OPTIONS,
  type SearchMode,
} from "../../config/search";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  searchMode: SearchMode;
  onSearchModeChange: (mode: SearchMode) => void;
  placeholder?: string;
}

function SearchBar({
  value,
  onChange,
  searchMode,
  onSearchModeChange,
  placeholder = "Search research papers...",
}: Readonly<SearchBarProps>) {
  return (
    <div
      className="search-control"
      role="search"
    >
      {/* Search Icon */}
      <span
        className="search-icon"
        aria-hidden="true"
      >
        🔍
      </span>

      {/* Search Input */}
      <input
        type="search"
        value={value}
        onChange={(event) =>
          onChange(event.target.value)
        }
        placeholder={placeholder}
        autoComplete="off"
        className="search-input"
        aria-label="Search research papers"
      />

      {/* Divider */}
      <span
        className="search-mode-divider"
        aria-hidden="true"
      />

      {/* Search Mode */}
      <select
        className="search-mode-select"
        value={searchMode}
        aria-label="Search mode"
        onChange={(event) =>
          onSearchModeChange(
            event.target.value as SearchMode,
          )
        }
      >
        {SEARCH_MODE_OPTIONS.map((option) => (
          <option
            key={option.value}
            value={option.value}
          >
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}

export default SearchBar;