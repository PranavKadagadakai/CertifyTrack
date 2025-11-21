import React, { useState, useEffect } from "react";
import api from "../api";

const AdminAICTEConfig = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    min_points_required: "",
    max_points_allowed: "",
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      const response = await api.get("/admin/aicte/");
      setCategories(response.data.results || response.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to load AICTE categories");
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setError("");
      const payload = {
        name: formData.name,
        description: formData.description,
        min_points_required: formData.min_points_required
          ? parseInt(formData.min_points_required)
          : null,
        max_points_allowed: formData.max_points_allowed
          ? parseInt(formData.max_points_allowed)
          : null,
      };

      if (editingId) {
        await api.patch(`/admin/aicte/${editingId}/`, payload);
        setSuccess("Category updated successfully!");
      } else {
        await api.post("/admin/aicte/", payload);
        setSuccess("Category created successfully!");
      }

      setFormData({
        name: "",
        description: "",
        min_points_required: "",
        max_points_allowed: "",
      });
      setShowCreateForm(false);
      setEditingId(null);
      fetchCategories();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to save category");
    }
  };

  const handleEdit = (category) => {
    setFormData({
      name: category.name,
      description: category.description,
      min_points_required: category.min_points_required || "",
      max_points_allowed: category.max_points_allowed || "",
    });
    setEditingId(category.id);
    setShowCreateForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this category?")) {
      try {
        await api.delete(`/admin/aicte/${id}/`);
        setSuccess("Category deleted successfully!");
        fetchCategories();
      } catch (err) {
        setError("Failed to delete category");
      }
    }
  };

  if (loading)
    return <div className="text-center py-10">Loading AICTE categories...</div>;

  return (
    <div className="space-y-6">
      {error && (
        <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      {success && (
        <div className="p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          {success}
        </div>
      )}

      {/* Create Button */}
      <div className="bg-white p-6 rounded-lg shadow">
        <button
          onClick={() => {
            setEditingId(null);
            setFormData({
              name: "",
              description: "",
              min_points_required: "",
              max_points_allowed: "",
            });
            setShowCreateForm(!showCreateForm);
          }}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          ➕ Create Category
        </button>
      </div>

      {/* Form */}
      {showCreateForm && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">
            {editingId ? "Edit" : "Create"} AICTE Category
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              placeholder="Category Name"
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
              required
              className="w-full px-4 py-2 border rounded-lg"
            />
            <textarea
              placeholder="Description"
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              className="w-full px-4 py-2 border rounded-lg"
              rows="3"
            />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="number"
                placeholder="Minimum Points (optional)"
                value={formData.min_points_required}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    min_points_required: e.target.value,
                  })
                }
                className="px-4 py-2 border rounded-lg"
              />
              <input
                type="number"
                placeholder="Maximum Points (optional)"
                value={formData.max_points_allowed}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    max_points_allowed: e.target.value,
                  })
                }
                className="px-4 py-2 border rounded-lg"
              />
            </div>
            <div className="flex gap-4">
              <button
                type="submit"
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                Save
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowCreateForm(false);
                  setEditingId(null);
                }}
                className="px-6 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Categories Table */}
      <div className="bg-white rounded-lg shadow overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-100 border-b">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-bold">Name</th>
              <th className="px-6 py-3 text-left text-sm font-bold">
                Description
              </th>
              <th className="px-6 py-3 text-left text-sm font-bold">
                Min Points
              </th>
              <th className="px-6 py-3 text-left text-sm font-bold">
                Max Points
              </th>
              <th className="px-6 py-3 text-left text-sm font-bold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {categories.map((category) => (
              <tr key={category.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-3 font-medium">{category.name}</td>
                <td className="px-6 py-3 text-gray-600">
                  {category.description}
                </td>
                <td className="px-6 py-3">
                  {category.min_points_required || "—"}
                </td>
                <td className="px-6 py-3">
                  {category.max_points_allowed || "—"}
                </td>
                <td className="px-6 py-3 space-x-2">
                  <button
                    onClick={() => handleEdit(category)}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(category.id)}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminAICTEConfig;
