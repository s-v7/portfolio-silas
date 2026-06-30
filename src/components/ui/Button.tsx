type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "default" | "primary";
};

const Button = ({ variant = "default", className = "", ...props }: Props) => (
  <button
    {...props}
    className={[
      "ds-btn",
      variant === "primary" ? "ds-btn-primary" : "",
      className,
    ].join(" ")}
  />
);

export default Button;

