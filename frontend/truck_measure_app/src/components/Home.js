import React, { useContext } from "react";
import "../styles/Home.css";  
import UserContext from "../auth/UserContext";
import { Link } from "react-router-dom";

/**
 * Renders the Home component.
 * @returns {JSX.Element} The rendered Home component.
 */
const Home = () => {
  const { currentUser } = useContext(UserContext);

  return (
    <div className="Homepage">
      <div className="container text-center">
        <h1 className="mb-4 font-weight-bold">Volvo Vision System</h1>
        {currentUser && (
          <h2>Welcome Back {currentUser.firstName || currentUser.username}!</h2>
        )}

        <p>
        Volvo trucks, renowned for their excellence in transportation, stand as a testament to innovation and reliability in the industry. With a history of unmatched performance and cutting-edge technology, Volvo trucks have become a symbol of quality and efficiency. These vehicles are more than just a mode of transportation; they represent a commitment to delivering goods safely and efficiently across the world. Volvo trucks, known for their robustness and advanced features, have earned the trust of businesses and drivers alike, making them a preferred choice for heavy-duty tasks.
        </p>
        
        <div className="image-container">
        <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.electrichybridvehicletechnology.com%2Fwp-content%2Fuploads%2F2020%2F11%2FVolvo-Trucks-cropped.jpg&f=1&nofb=1&ipt=673fe46bba5440501c483418c17b362249a44db956a11a327e6b5ad1938ca584&ipo=imagese.jpg" alt="A dog playing in the park" />
        <img src="https://fleetnews.gr/wp-content/uploads/2021/04/Volvo-Trucks_08A6145.jpg" alt="A sunset viewed from the beach" />
        </div>
      </div>
    </div>
  );
}

export default Home;
