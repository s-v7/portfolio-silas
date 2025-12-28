
interface UserImageProPros {
	src: string;
	alt: string;
}

const UserImagePro: React.FC<UserImageProPros> = ({ src, alt }) => {
      	return (
    		<div className="user-image-container">
	  		<img src={src} alt={alt} className="user-image" />
	    	</div>
      	);
};

export default UserImagePro;
