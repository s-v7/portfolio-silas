type Props = {
  children: React.ReactNode;
  className?: string;
};

const Card = ({ children, className = "" }: Props) => (
  <div className={`ds-card ds-card-pad ${className}`}>
    {children}
  </div>
);

export default Card;

