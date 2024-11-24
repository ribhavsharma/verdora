"use client";
import React, { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface User {
  username: string;
  email: string;
  phone_number: string;
  avatar: string;
  wishlist: Array<string>;
}

interface Item {
  id: number;
  category: string;
}

const ProfilePage = () => {
  const [user, setUser] = useState<User | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState<User | null>(null);
  const [items, setItems] = useState<Item[]>([]); // State for user item listings

  const wishlistItems = [  'Accessories','Shoes','Clothes','Bags','Glassware', 'Lightbulb',  
    'Aluminium Foil or Tray', 'Metal Can or Container',  
    'Cardboard', 'Battery', 'Electronic Waste',];

  useEffect(() => {
    const storedUsername = localStorage.getItem("user");

    if (storedUsername) {
      fetch("http://127.0.0.1:8000/userDetails", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: storedUsername }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data) {
            const userData = {
              username: data.name,
              email: data.email,
              phone_number: data.phone_number,
              avatar: data.avatar || "https://via.placeholder.com/150",
              wishlist: data.wishlist || ""
            };
            setUser(userData);
            setEditedUser(userData); // Initialize editedUser

            // Update items from the response
            if (data.listings) {
              setItems(data.listings);
            }
          }
        })
        .catch((error) => {
          console.log("Error fetching user details:", error);
        });
    }
  }, []);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditedUser(user); // Reset changes
  };

  const testSellItem = () => {
    fetch("http://127.0.0.1:8000/sellItem", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        item_name: "Shoes",
        username: editedUser?.username,
      }),
    })
  }

  const handleSave = async () => {
    if (editedUser) {
      try {
        const { avatar, ...userDetails } = editedUser;
        console.log(editedUser);
        const response = await fetch("http://127.0.0.1:8000/updateUser", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(userDetails),
        });

        if (response.ok) {
          setUser(editedUser);
          setIsEditing(false);
        } else {
          alert("Failed to update user details");
        }
      } catch (error) {
        alert("Error updating user details");
      }
    }
  };

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#BACBB3]">
        <Card className="w-full max-w-md">
          <CardContent className="p-6">
            <p className="text-center text-[#226f54]">
              Please log in to view your profile.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#BACBB3] p-4">
      {/* Wider container for cards */}
      <div className="w-full max-w-4xl space-y-10">
        {/* Profile Card */}
        <Card className="w-full">
          <CardHeader className="pb-4">
            <div className="flex items-center space-x-4">
              <Avatar className="w-16 h-16">
                <AvatarImage
                  src={`https://api.dicebear.com/6.x/initials/svg?seed=${user.username}`}
                  alt={user.username}
                />
                <AvatarFallback>{user.username.charAt(0)}</AvatarFallback>
              </Avatar>
              <CardTitle className="text-2xl font-bold text-[#226f54]">
                {user.username}
              </CardTitle>
            </div>
            <button onClick={testSellItem} >sakosaokokas</button>
          </CardHeader>
          <CardContent>
            <h2 className="text-xl font-semibold mb-4 text-[#226f54]">
              Contact Information
            </h2>
            <div className="space-y-2">
              <p className="text-[#43291f]">
                <strong>Email:</strong>{" "}
                {isEditing ? (
                  <Input
                    value={editedUser?.email || ""}
                    onChange={(e) =>
                      setEditedUser((prev) => (prev ? { ...prev, email: e.target.value } : null))
                    }
                    className="text-[#43291f]"
                  />
                ) : (
                  user.email
                )}
              </p>
              <p className="text-[#43291f]">
                <strong>Phone:</strong>{" "}
                {isEditing ? (
                  <Input
                    value={editedUser?.phone_number || ""}
                    onChange={(e) =>
                      setEditedUser((prev) =>
                        prev ? { ...prev, phone_number: e.target.value } : null
                      )
                    }
                    className="text-[#43291f]"
                  />
                ) : (
                  user.phone_number
                )}
              </p>
              <p className="text-[#43291f]">
                <strong>Wishlist:</strong>{" "}
                {isEditing ? (
                  <div>
                    {wishlistItems.map((item, index) => (
                      <label key={index} className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={editedUser?.wishlist?.includes(item) || false}
                          onChange={(e) => {
                            setEditedUser((prev) => {
                              if (!prev) return null;
                              const updatedWishlist = e.target.checked
                                ? [...(prev.wishlist || []), item] // Add item
                                : (prev.wishlist || []).filter((i: string) => i !== item); // Remove item
                              return { ...prev, wishlist: updatedWishlist };
                            });
                          }}
                          className="text-[#43291f]"
                        />
                        <span>{item}</span>
                      </label>
                    ))}
                  </div>
                ) : (
                  user.wishlist.join(", ")
                )}
              </p>
            </div>
            {isEditing ? (
              <div className="mt-4 flex space-x-4">
                <Button
                  onClick={handleSave}
                  className="bg-[#226f54] hover:bg-[#87c38f] text-white"
                >
                  Save
                </Button>
                <Button
                  onClick={handleCancel}
                  className="bg-[#43291f] hover:bg-[#87c38f] text-white"
                >
                  Cancel
                </Button>
              </div>
            ) : (
              <div className="mt-4">
                <Button
                  onClick={handleEdit}
                  className="bg-[#226f54] hover:bg-[#87c38f] text-white"
                >
                  Edit
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* My Item Listings Section */}
        <Card className="w-full">
          <CardHeader>
            <CardTitle className="text-xl font-bold text-[#226f54]">
              My Item Listings
            </CardTitle>
          </CardHeader>
          <CardContent>
            {items.length > 0 ? (
              <ul className="space-y-2">
                {items.map((item, index) => (
                  <li
                    key={index}
                    className="flex justify-between items-center p-3 bg-gray-100 rounded-md"
                  >
                    <p className="font-medium text-[#226f54]">{item.category}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-[#43291f]">No items listed yet.</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProfilePage;
