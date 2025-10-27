import React from "react";

const UserImagePro = ({ src, alt }) => {
  return (
    <div className="user-image-container">
      <img src={src} alt={alt} className="user-image" />
    </div>
  );
};

export default UserImagePro;
