import React, { ReactNode } from "react";

export interface ModalProps {
  open: boolean;
  title: string;
  onClose: () => void;
  children?: ReactNode;
}

const Modal: React.FC<ModalProps> = ({
  open,
  title,
  onClose,
  children,
}) => {
  if (!open) return null;

  return (
    <div className="ds-overlay">
      <div className="ds-modal">
        <header className="mb-4 flex items-center justify-between">
          <h3 className="text-lg font-semibold">{title}</h3>
          <button
            onClick={onClose}
            className="text-sm text-[var(--muted)] hover:text-[var(--text)]"
          >
            ✕
          </button>
        </header>

        <div>{children}</div>
      </div>
    </div>
  );
};


export default Modal;

