"use client";

import { useParams } from "next/navigation";
import React, { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

const Page = ({ params }: { params: { itemId: string } }) => {
 
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      marketplace !!!
    </div>
  );
};

export default Page;
