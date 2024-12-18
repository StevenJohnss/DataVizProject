import React from 'react';
import { motion } from 'framer-motion';
import { Link, NavLink } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import { useNavigate } from 'react-router-dom';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/signin');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <Link to="/" className="flex-shrink-0 flex items-center">
                <img className="h-8 w-auto" src="logo192.png" alt="Logo" />
              </Link>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <NavLink
                  to="/"
                  className={({ isActive }) =>
                    `${isActive ? 'border-indigo-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`
                  }
                >
                  Dashboard
                </NavLink>
                <NavLink
                  to="/sales"
                  className={({ isActive }) =>
                    `${isActive ? 'border-indigo-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`
                  }
                >
                  Sales
                </NavLink>
                <NavLink
                  to="/images"
                  className={({ isActive }) =>
                    `${isActive ? 'border-indigo-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`
                  }
                >
                  Images
                </NavLink>
                <NavLink
                  to="/profile"
                  className={({ isActive }) =>
                    `${isActive ? 'border-indigo-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`
                  }
                >
                  Profile
                </NavLink>
              </div>
            </div>
            {isAuthenticated && (
              <button onClick={handleLogout} className="text-gray-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium hover:bg-purple-200 rounded-md">
                Logout
              </button>
            )}
          </div>
        </div>
      </nav>
      <main>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          {children}
        </motion.div>
      </main>
    </div>
  );
};

export default Layout;
