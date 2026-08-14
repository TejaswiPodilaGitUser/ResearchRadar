import type { Topic } from "../../types/topic";

interface TopicCardProps {
  topic: Topic;
  onClick?: (topicId: number) => void;
}

function TopicCard({
  topic,
  onClick,
}: Readonly<TopicCardProps>) {
  const handleClick = (): void => {
    if (onClick !== undefined) {
      onClick(topic.topic_id);
    }
  };

  return (
    <article className="entity-card">

      <div className="entity-card-header">
        <span className="entity-card-id">
          Topic ID: {topic.topic_id}
        </span>
      </div>

      <h3 className="entity-card-title">
        {topic.topic_name}
      </h3>

      {onClick !== undefined && (
        <button
          type="button"
          className="entity-card-action"
          onClick={handleClick}
        >
          <span>
            View Topic
          </span>
          <span aria-hidden="true">
            →
          </span>
        </button>
      )}

    </article>
  );
}

export default TopicCard;