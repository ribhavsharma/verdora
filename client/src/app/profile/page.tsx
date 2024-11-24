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
}

const ProfilePage = () => {
  const [user, setUser] = useState<User | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState<User | null>(null);

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
              phone_number: data.phone,
              avatar: data.avatar || "https://via.placeholder.com/150",
            };
            setUser(userData);
            setEditedUser(userData); // Initialize editedUser
          }
        })
        .catch((error) => {
          console.log("error");
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

  const handleSave = async () => {
    if (editedUser) {
      try {
        const { avatar, ...userDetails } = editedUser;
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
    <div className="flex items-center justify-center min-h-screen bg-[#BACBB3] p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="pb-4">
          <div className="flex items-center space-x-4">
            <Avatar className="w-16 h-16">
              <AvatarImage src={`https://api.dicebear.com/6.x/initials/svg?seed=${user.username}`} alt={user.username} />
              <AvatarFallback>{user.username.charAt(0)}</AvatarFallback>
            </Avatar>
            <CardTitle className="text-2xl font-bold text-[#226f54]">
              {user.username}
            </CardTitle>
          </div>
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
                    setEditedUser((prev) => ({
                      ...prev!,
                      email: e.target.value,
                    }))
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
                    setEditedUser((prev) => ({
                      ...prev!,
                      phone_number: e.target.value, // Update the correct key
                    }))
                  }
                  className="text-[#43291f]"
                />
              ) : (
                user.phone_number
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
    </div>
  );
};

export default ProfilePage;
