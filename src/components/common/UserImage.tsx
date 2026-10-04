const userPhoto = "/logo.svg";

const UserImage: React.FC = () => {
  return (
    <div className="user-image-container">
      <img src={userPhoto} alt="Minha Foto" className="user-image" loading="lazy" />
    </div>
  );
};

export default UserImage;
