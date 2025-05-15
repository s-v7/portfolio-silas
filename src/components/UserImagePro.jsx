import React from "react";
import "./UserImagePro.css"; // Arquivo de estilos específico

const UserImagePro = ({ src, alt }) => {
  return (
    <div className="user-image-container">
      <img src={src} alt={alt} className="user-image" />
    </div>
  );
};

export default UserImagePro;

