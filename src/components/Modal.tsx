import React from "react";

interface ModalProps {
  title: string;
  content: React.ReactNode;
  onClose: () => void;
}

const Modal: React.FC<ModalProps> = ({ title, content, onClose }) => {
  return (
    <div
      className="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center"
      role="dialog"
      aria-modal="true"
    >
      <div className="bg-white p-6 rounded shadow-lg max-w-md w-full">
        <h2 className="text-xl font-bold mb-4">{title}</h2>

        <div>{content}</div>

        <button
          onClick={onClose}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          aria-label="Close modal"
        >
          Fechar
        </button>
      </div>
    </div>
  );
};

export default Modal;

