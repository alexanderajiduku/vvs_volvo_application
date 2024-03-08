import { io } from "socket.io-client";

const socket = io("http://localhost:8000", { path: 'ws/socket.io/', autoConnect: true });

export default socket;
