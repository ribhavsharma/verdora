interface DonationCenter {
    name: string;
    link: string; 
    address: string; 
    contact: string; 
}
const DonationCentersRepo: Record<string, DonationCenter[]> = {
    clothes: [
      {
        name: "Salvation Army",
        link: "kelownasalvationarmy.ca",
        address: "1480 Sutherland Ave, Kelowna, BC, V1Y 5Y5",
        contact: "250.860.2329",
      },
      {
        name: "Value Village",
        link: "https://stores.savers.com/bc/kelowna/",
        address: "190 Aurora Crescent Kelowna, BC V1X 7M3",
        contact: "250.491.1356",
      },
    ],
    eWaste: [
      {
        name: "Tech Recycle Hub",
        link: "https://techrecycle.example.com",
        address: "789 Tech Park, Silicon City",
        contact: "555-123-4567",
      },
    ],
    food: [
      {
        name: "Community Food Bank",
        link: "https://foodbank.example.com",
        address: "321 Helping Hand Blvd, Kindness Town",
        contact: "111-222-3333",
      },
    ],
};
  
  export default DonationCentersRepo;
  