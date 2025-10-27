import React from "react";
import userPhoto from "../logo.svg"; //user-photo.jpg";

const UserImage = () => {
  return (
    <div className="user-image-container">
      <img src={userPhoto} alt="Minha Foto" className="user-image" />
    </div>
  );
};

export default UserImage;
