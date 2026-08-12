interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit?: () => void;
  placeholder?: string;
}

function SearchBar({
  value,
  onChange,
  onSubmit,
  placeholder = "Search research papers...",
}: Readonly<SearchBarProps>) {
  const handleSubmit = (
    event: React.SyntheticEvent<HTMLFormElement>,
  ): void => {
    event.preventDefault();
    onSubmit?.();
  };

  return (
    <form
      onSubmit={handleSubmit}
      role="search"
      style={{
        display: "flex",
        gap: "12px",
        alignItems: "stretch",
      }}
    >
      <div className="search-input-wrapper">
        <span className="search-icon">🔍</span>

        <input
          type="search"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder={placeholder}
          autoComplete="off"
          className="search-input"
        />
      </div>

      <button type="submit" className="search-button">
        Search
      </button>
    </form>
  );
}

export default SearchBar;