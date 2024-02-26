import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "../components/Home"; // Homepage
import SignupForm from "../auth/SignupForm";
import SigninForm from "../auth/SigninForm";
import ProtectedComponent from "../components/ProtectedComponent";
import PrivateRoute from "./PrivateRoute";
import NotFound from "./NotFound"; // 404 component

const AppRoutes = () => {
  return (
    <div className="pt-5">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signin" element={<SigninForm />} />
        <Route path="/signup" element={<SignupForm />} />
        <Route
          path="/protected"
          element={
            <PrivateRoute>
              <ProtectedComponent />
            </PrivateRoute>
          }
        />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
};

export default AppRoutes;
