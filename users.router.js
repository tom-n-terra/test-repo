const express = require('express');
const router = express.Router();

// Mock data - in real app, this would be your database
let users = [
  { id: 1, name: 'John Doe', email: 'john@example.com', age: 30 },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', age: 25 },
  { id: 3, name: 'Mike Johnson', email: 'mike@example.com', age: 35 }
];

// GET /users - Get all users
const getAllUsers = (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;
    const startIndex = (page - 1) * limit;
    const endIndex = page * limit;
    
    const paginatedUsers = users.slice(startIndex, endIndex);
    
    res.status(200).json({
      success: true,
      data: paginatedUsers,
      total: users.length,
      page: parseInt(page),
      totalPages: Math.ceil(users.length / limit)
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Server error',
      error: error.message
    });
  }
};

// GET /users/:id - Get user by ID
const getUserById = (req, res) => {
  try {
    const { id } = req.params;
    const user = users.find(u => u.id === parseInt(id));
    
    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }
    
    res.status(200).json({
      success: true,
      data: user
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Server error',
      error: error.message
    });
  }
};

// POST /users - Create new user
const createUser = (req, res) => {
  try {
    const { name, email, age } = req.body;
    
    // Basic validation
    if (!name || !email) {
      return res.status(400).json({
        success: false,
        message: 'Name and email are required'
      });
    }
    
    // Check if email already exists
    const existingUser = users.find(u => u.email === email);
    if (existingUser) {
      return res.status(400).json({
        success: false,
        message: 'Email already exists'
      });
    }
    
    // Create new user
    const newUser = {
      id: users.length > 0 ? Math.max(...users.map(u => u.id)) + 1 : 1,
      name,
      email,
      age: age || null
    };
    
    users.push(newUser);
    
    res.status(201).json({
      success: true,
      message: 'User created successfully',
      data: newUser
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Server error',
      error: error.message
    });
  }
};

// PUT /users/:id - Update user
const updateUser = (req, res) => {
  try {
    const { id } = req.params;
    const { name, email, age } = req.body;
    
    const userIndex = users.findIndex(u => u.id === parseInt(id));
    
    if (userIndex === -1) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }
    
    // Check if email already exists (excluding current user)
    if (email) {
      const existingUser = users.find(u => u.email === email && u.id !== parseInt(id));
      if (existingUser) {
        return res.status(400).json({
          success: false,
          message: 'Email already exists'
        });
      }
    }
    
    // Update user
    const updatedUser = {
      ...users[userIndex],
      ...(name && { name }),
      ...(email && { email }),
      ...(age !== undefined && { age })
    };
    
    users[userIndex] = updatedUser;
    
    res.status(200).json({
      success: true,
      message: 'User updated successfully',
      data: updatedUser
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Server error',
      error: error.message
    });
  }
};

// DELETE /users/:id - Delete user
const deleteUser = (req, res) => {
  try {
    const { id } = req.params;
    const userIndex = users.findIndex(u => u.id === parseInt(id));
    
    if (userIndex === -1) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }
    
    const deletedUser = users.splice(userIndex, 1)[0];
    
    res.status(200).json({
      success: true,
      message: 'User deleted successfully',
      data: deletedUser
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Server error',
      error: error.message
    });
  }
};

// Route definitions
router.get('/', getAllUsers);
router.get('/:id', getUserById);
router.post('/', createUser);
router.put('/:id', updateUser);
router.delete('/:id', deleteUser);

module.exports = {
  router,
  getAllUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser
};
