"use client";

import { useRef, useState, useEffect } from "react";
import { Camera, X, Upload, Loader2, PackagePlus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Toaster } from "@/components/ui/toaster";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { toast } from "@/hooks/use-toast";

interface Result {
  image: string;
  className: string;
}

export default function CameraApp() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [photo, setPhoto] = useState<string | null>(null);
  const [isMobile, setIsMobile] = useState(false);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [results, setResults] = useState<Result[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const donationCenters: Record<string, string> = {
    e_waste: "Find e-waste donation centers at: https://example.com/e-waste",
    recyclable: "Visit your nearest recycling center: https://example.com/recycle",
    compostable: "Locate composting facilities here: https://example.com/compost",
  };

  useEffect(() => {
    const userAgent = navigator.userAgent;
    setIsMobile(/android|iphone|ipad|ipod/i.test(userAgent));

    const signedIn = localStorage.getItem("auth");
    if (!signedIn) {
      window.location.href = "/auth";
    }
  }, []);

  useEffect(() => {
    if (isCameraActive && !isMobile) {
      const setupCamera = async () => {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
          });
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            videoRef.current.play();
          }
        } catch (err) {
          console.error("Error accessing camera:", err);
          alert("Unable to access camera. Please check permissions.");
        }
      };
      setupCamera();
    }
  }, [isCameraActive, isMobile]);

  const startCamera = () => {
    if (isMobile) {
      fileInputRef.current?.click();
    } else {
      setIsCameraActive(true);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      const tracks = stream.getTracks();

      tracks.forEach((track) => track.stop());
      videoRef.current.srcObject = null;
      setIsCameraActive(false);
    }
  };

  const capturePhoto = () => {
    if (!isMobile && videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const context = canvas.getContext("2d");

      if (context) {
        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;
        context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

        const imageURL = canvas.toDataURL("image/png");
        setPhoto(imageURL);
        stopCamera();
        handleApiCall(imageURL);
      }
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      const imageURL = URL.createObjectURL(files[0]);
      setPhoto(imageURL);
      handleApiCall(imageURL);
    }
  };

  const handleApiCall = async (imageUrl: string) => {
    setIsLoading(true);

    await new Promise((resolve) => setTimeout(resolve, 1500));
    const mockResults = [
      { image: imageUrl, className: "recyclable" },
      { image: imageUrl, className: "compostable" },
      { image: imageUrl, className: "e_waste" },
    ];

    setResults(mockResults);
    setIsLoading(false);
  };

  const handleSell = async (index: number) => {
    const result = results[index];
    const itemName = result.className.toLowerCase();
    const image = result.image;

    const username = localStorage.getItem("user");

    if (!username) {
      alert("User not logged in.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/sellItem", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          item_name: itemName,
          username: username,
          image: image,
        }),
      });

      if (response.ok) {
        toast({
          title: "Success!",
          description: "Item added to marketplace.",
        });
      } else {
        const errorData = await response.json();
        alert(errorData.detail || "Failed to sell the item.");
      }
    } catch (error) {
      console.error("Error selling item:", error);
      alert("Failed to connect to the server.");
    }
  };

  return (
    <div className="min-h-screen bg-[#BACBB3] p-4 md:p-8">
      <Card className="max-w-5xl mx-auto bg-white shadow-xl rounded-xl overflow-hidden">
        <CardContent className="p-6 md:p-8">
          <h1 className="text-3xl font-bold text-center text-[#226F54] mb-8">
            verdora
          </h1>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="space-y-6">
              <Tabs defaultValue="camera" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="camera">Camera</TabsTrigger>
                  <TabsTrigger value="upload">Upload</TabsTrigger>
                </TabsList>
                <TabsContent value="camera">
                  <div className="aspect-video bg-gray-100 rounded-lg overflow-hidden relative">
                    <video
                      ref={videoRef}
                      className={`absolute inset-0 w-full h-full object-cover ${
                        isCameraActive ? "" : "hidden"
                      }`}
                    />
                    {!isCameraActive && (
                      <div className="flex items-center justify-center h-full">
                        <Camera className="w-16 h-16 text-gray-400" />
                      </div>
                    )}
                  </div>
                  <div className="mt-4 flex justify-center">
                    <Button
                      onClick={isCameraActive ? capturePhoto : startCamera}
                      className="bg-[#226F54] text-white hover:bg-[#87C38F] transition-all"
                      size="lg"
                    >
                      {isCameraActive ? (
                        <>
                          <Camera className="mr-2 h-5 w-5" />
                          Capture Photo
                        </>
                      ) : (
                        <>
                          <Camera className="mr-2 h-5 w-5" />
                          Start Camera
                        </>
                      )}
                    </Button>
                    {isCameraActive && (
                      <Button
                        onClick={stopCamera}
                        className="ml-4 bg-[#43291F] text-white hover:bg-[#87C38F] transition-all"
                        size="lg"
                      >
                        <X className="mr-2 h-5 w-5" />
                        Stop Camera
                      </Button>
                    )}
                  </div>
                </TabsContent>
                <TabsContent value="upload">
                  <div
                    className="aspect-video bg-gray-100 rounded-lg overflow-hidden flex items-center justify-center cursor-pointer"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <div className="text-center">
                      <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-500">Click to upload an image</p>
                    </div>
                  </div>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                </TabsContent>
              </Tabs>

              {photo && (
                <div className="space-y-4">
                  <h2 className="text-xl font-semibold text-[#226F54]">
                    Captured Photo
                  </h2>
                  <div className="aspect-video w-full relative rounded-lg overflow-hidden">
                    <img
                      src={photo}
                      alt="Captured"
                      className="absolute inset-0 w-full h-full object-cover"
                    />
                  </div>
                </div>
              )}
            </div>

            <div className="space-y-6">
              <h2 className="text-2xl font-semibold text-[#226F54]">Results</h2>
              {isLoading ? (
                <div className="flex items-center justify-center h-64">
                  <Loader2 className="w-8 h-8 text-[#226F54] animate-spin" />
                </div>
              ) : results.length > 0 ? (
                <div className="space-y-4">
                  {results.map((result, index) => (
                    <div
                      key={index}
                      className="flex flex-col gap-4 bg-gray-50 p-4 rounded-lg"
                    >
                      <div className="flex items-center gap-4">
                        <div className="w-16 h-16 shrink-0">
                          <img
                            src={result.image}
                            alt={result.className}
                            className="w-full h-full object-cover rounded-md"
                          />
                        </div>
                        <div className="flex-1">
                          <p className="text-[#43291F] font-medium">
                            {result.className}
                          </p>
                          <p className="text-sm text-gray-500">
                            Confidence: 95%
                          </p>
                        </div>
                      </div>
                      <p className="text-sm text-gray-700">
                        {donationCenters[result.className.toLowerCase()] ||
                          "No specific recommendation available for this type."}
                      </p>
                      <div className="flex items-center gap-2">
                        <TooltipProvider>
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                size="icon"
                                variant="ghost"
                                className="text-[#226F54] hover:bg-[#87C38F]"
                                onClick={() => handleSell(index)}
                              >
                                <PackagePlus className="h-5 w-5" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>
                              <p>Sell this item</p>
                            </TooltipContent>
                          </Tooltip>
                        </TooltipProvider>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center">
                  No results yet. Capture or upload an image to get started.
                </p>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
}
