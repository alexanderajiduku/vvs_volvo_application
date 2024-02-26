// PrivatePage.js

import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import ProtectedComponent from './ProtectedComponent'; 

const ProtectedComponent = () => {
  return (
    <div>
      <nav>
        <Link to="/protected/component">Protected Component</Link>
      </nav>
      <Routes>
        <Route path="component" element={<ProtectedComponent />} />
      </Routes>
    </div>
  );
};

export default ProtectedComponent;