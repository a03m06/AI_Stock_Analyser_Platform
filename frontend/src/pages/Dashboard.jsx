export default function Dashboard() {

    return (
        <div style={{
            display: "flex",
            height: "100vh"
        }}>

            <div style={{
                width: "300px",
                borderRight: "1px solid gray",
                padding: "20px"
            }}>
                Filters
            </div>

            <div style={{
                flex: 1,
                padding: "20px"
            }}>
                Rankings
            </div>

            <div style={{
                width: "400px",
                borderLeft: "1px solid gray",
                padding: "20px"
            }}>
                Company Details
            </div>

        </div>
    );
}