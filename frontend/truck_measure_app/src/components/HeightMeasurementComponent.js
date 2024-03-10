// import React, { useState, useEffect } from "react";
// import io from "socket.io-client";

// const SOCKET_SERVER_URL = "http://localhost:8000";

// const HeightMeasurementComponent = () => {
//   const [heightMeasurements, setHeightMeasurements] = useState([]);

//   useEffect(() => {
//     const socket = io(SOCKET_SERVER_URL);

//     // Event listener for connecting to the socket server
//     socket.on("connect", () => {
//       console.log("Connected to server");
//     });

//     // Event listener for receiving height measurements
//     socket.on("height_measurement", (data) => {
//       console.log("Received height measurement:", data);
//       setHeightMeasurements((prevMeasurements) => [...prevMeasurements, data]);
//     });

//     // Cleanup function to disconnect from the socket server when the component unmounts
//     return () => {
//       socket.disconnect();
//     };
//   }, []); // Empty dependency array ensures this effect runs only once on component mount

//   return (
//     <div>
//       <h1>Height Measurements</h1>
//       <ul>
//         {heightMeasurements.map((measurement, index) => (
//           <li key={index}>
//             Vehicle ID: {measurement.vehicle_id}, Height: {measurement.height}
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default HeightMeasurementComponent;
