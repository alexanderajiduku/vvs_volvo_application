import React from "react";
import { Route, Routes, Navigate } from "react-router-dom";
import Home from "../components/Home";
import SignupForm from "../auth/SignupForm";
import PrivateRoute from "./PrivateRoute"; 
import Calibration from "../components/Calibration";
import MLModel from "../components/MLModel";
import AIProcesses from "../components/AIProcesses"; 
import SigninForm from "../auth/SigninForm";
import Ultralytics from "../components/Ultralytics";
import TruckMeasure from "../components/TruckMeasure";

const RoutesNav = ({signin, signup}) => {
    return (
        <div className="pt-5">
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/signin" element={<SigninForm />} />
                <Route path="/signup" element={<SignupForm />} />

                <Route path="/calibration" element={
                    <PrivateRoute>
                        <Calibration />
                    </PrivateRoute>
                } />
                <Route path="/mlmodel" element={
                    <PrivateRoute>
                        <MLModel />
                    </PrivateRoute>
                } />
                <Route path="/aiprocesses" element={
                    <PrivateRoute>
                        <AIProcesses /> 
                    </PrivateRoute>
                } />
                <Route path="/ultralytics" element={
                    <PrivateRoute>
                        <Ultralytics />
                    </PrivateRoute>
                } />
                  <Route path="/truckmeasure" element={
                    <PrivateRoute>
                        <TruckMeasure />
                    </PrivateRoute>
                } />
                <Route path="/*" element={<Navigate to="/" />} />
            </Routes>
        </div>
    );
};

export default RoutesNav;
