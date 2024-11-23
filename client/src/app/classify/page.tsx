"use client";

import { useRef, useState, useEffect } from "react";

export default function CameraApp() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [photo, setPhoto] = useState<string | null>(null);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const userAgent = navigator.userAgent;
    setIsMobile(/android|iphone|ipad|ipod/i.test(userAgent));
  }, []);

  const startCamera = async () => {
    if (isMobile) {
      fileInputRef.current?.click();
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
        }
      } catch (err) {
        console.error("Error accessing camera:", err);
        alert("Unable to access camera. Please check permissions.");
      }
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      const tracks = stream.getTracks();

      tracks.forEach((track) => track.stop());
      videoRef.current.srcObject = null;
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
      }
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      const imageURL = URL.createObjectURL(files[0]);
      setPhoto(imageURL);
    }
    // TODO: Send the image to the server for classification
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#f4f0bb] p-5">
      <h1 className="text-4xl font-bold mb-6 text-[#226f54]">verdora</h1>
      <div className="flex flex-col items-center justify-center w-full max-w-lg">
        {!isMobile && (
          <div className="relative w-full h-72 bg-[#43291f] rounded-lg overflow-hidden mb-6">
            <video
              ref={videoRef}
              className="absolute top-0 left-0 w-full h-full object-cover"
            />
          </div>
        )}

        <div className="flex space-x-4 mb-6">
          <button
            onClick={startCamera}
            className="bg-[#226f54] text-[#f4f0bb] px-4 py-2 rounded-lg shadow-md hover:bg-[#87c38f] hover:text-[#43291f] transition-all"
          >
            {isMobile ? "Open Camera" : "Start Camera"}
          </button>
          {!isMobile && (
            <button
              onClick={capturePhoto}
              className="bg-[#87c38f] text-[#43291f] px-4 py-2 rounded-lg shadow-md hover:bg-[#226f54] hover:text-[#f4f0bb] transition-all"
            >
              Capture Photo
            </button>
          )}
          <button
            onClick={stopCamera}
            className="bg-[#43291f] text-[#f4f0bb] px-4 py-2 rounded-lg shadow-md hover:bg-[#87c38f] hover:text-[#43291f] transition-all"
          >
            Stop Camera
          </button>
        </div>

        {photo && (
          <div className="text-center">
            <h2 className="text-2xl font-semibold mb-4 text-[#226f54]">
              Captured Photo
            </h2>
            <img
              src={photo}
              alt="Captured"
              className="w-full max-w-[400px] border-2 border-[#87c38f] rounded-lg mx-auto"
            />
          </div>
        )}
      </div>

      {isMobile && (
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleFileChange}
          className="hidden"
        />
      )}

      {!isMobile && <canvas ref={canvasRef} style={{ display: "none" }} />}
    </div>
  );
}

