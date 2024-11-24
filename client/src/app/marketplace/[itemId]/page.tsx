"use client";

import { useParams } from "next/navigation";
import React, { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { toast } from "@/hooks/use-toast";

const Page = ({ params }: { params: { itemId: string } }) => {
  const { itemId } = useParams();
  const [itemDetails, setItemDetails] = useState<any>(null);
  const [isSeller, setIsSeller] = useState(false);

  useEffect(() => {
    const fetchItemDetails = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/getItemDetails`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ itemId }),
        });
        const data = await response.json();
        setItemDetails(data);

        const loggedUser = localStorage.getItem("user");
        if (loggedUser && data.seller_contact.username === loggedUser) {
          setIsSeller(true);
        }
      } catch (error) {
        console.error("Error fetching item details:", error);
      }
    };

    fetchItemDetails();
  }, [itemId]);

  const handleMarkAsSold = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/markAsSold`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ itemId }),
      });
      if (response.ok) {
        toast({
          title: "Success",
          description: "Item has been marked as sold.",
        });
      } else {
        toast({
          title: "Error",
          description: "Failed to mark item as sold.",
        });
      }
    } catch (error) {
      console.error("Error marking item as sold:", error);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-full max-w-2xl shadow-lg">
        <CardHeader>
          <CardTitle className="text-xl font-semibold text-gray-800">Item Details</CardTitle>
        </CardHeader>
        <CardContent>
          {itemDetails ? (
            <div className="space-y-4">
              <div>
                <p className="text-gray-600">
                  <strong>Item ID:</strong> {itemId}
                </p>
              </div>
              <Separator />
              <div>
                <p className="text-gray-600">
                  <strong>Category:</strong> {itemDetails.category}
                </p>
                <p className="text-gray-600">
                  <strong>Price:</strong> ${itemDetails.price}
                </p>
              </div>
              <Separator />
              <div>
                <h3 className="text-lg font-semibold text-gray-800">Seller Contact</h3>
                <p className="text-gray-600">
                  <strong>Email:</strong> {itemDetails.seller_contact.email}
                </p>
                <p className="text-gray-600">
                  <strong>Phone:</strong> {itemDetails.seller_contact.phone_number}
                </p>
              </div>
            </div>
          ) : (
            <p className="text-gray-600">Loading item details...</p>
          )}
        </CardContent>
        <CardFooter>
          {isSeller && (
             <Alert className="border-red-500 bg-red-50 text-red-700">
             <AlertTitle className="font-bold">Mark Item as Sold</AlertTitle>
             <AlertDescription>
               Are you sure you want to mark this item as sold? This action cannot be undone.
             </AlertDescription>
             <div className="mt-4 flex space-x-2">
               <Button variant="outline" className="hover:bg-gray-200">
                 Cancel
               </Button>
               <Button
                 className="bg-red-500 text-white hover:bg-red-600"
                 onClick={handleMarkAsSold}
               >
                 Confirm
               </Button>
             </div>
           </Alert>
          )}
        </CardFooter>
      </Card>
    </div>
  );
};

export default Page;
