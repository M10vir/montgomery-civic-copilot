export default function AddressLookupCard({ data }) {
  return (
    <section className="card">
      <h2>Lookup Result</h2>
      <p className="box">
        <b>Address:</b> {data.address} <br />
        <b>District:</b> {data.district} <br />
        <b>Representative:</b> {data.representative}
      </p>
    </section>
  );
}
