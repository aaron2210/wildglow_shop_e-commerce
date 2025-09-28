export const Categorias = () => {
    return (
        <>
            <div className="container-fluid py-4 position-relative z-1">
                <h5 className="fw-bold text-center">Categorías</h5>
                <p className="text-center">
                    Explora nuestras colecciones y encuentra lo que mejor se adapta a tu estilo: <br />
                    velas aromáticas, wax melts y accesorios para crear ambientes únicos.
                </p>

                <div className="row bg-light-pink text-center position-relative overflow-visible px-5 py-5">


                    <div className="col-sm-12 col-md-4 mb-1 mb-lg-4 d-flex justify-content-center">
                        <div className="category-card raised">
                            <img className="img-fluid rounded" src="src/front/assets/img/WaxMelt-Box-Cherry-Crush_420234fa-fab5-4858-92a7-4208072268ca.webp" alt="wax melts" />
                            <h6 className="mt-2 fw-bold mt-lg-3">Wax Melts</h6>
                            <p className="mt-lg-4">Disfruta de fragancias intensas sin llama. Nuestros wax melts llenan tu hogar de aroma en segundos, ideales para momentos de calma y bienestar.</p>
                        </div>
                    </div>


                    <div className="col-sm-12 col-md-4 mb-4 d-flex justify-content-center">
                        <div className="category-card lowered text-center">
                            <img className="img-fluid rounded" src="src/front/assets/img/Velas-aromaticas.webp" alt="velas aromaticas" />
                            <h6 className="mt-2 fw-bold mt-lg-3">Velas Aromáticas</h6>
                            <p className="mt-lg-4">Transforma tu espacio con el encanto de nuestras velas aromáticas. Cada vela está diseñada para crear una atmósfera cálida, relajante y acogedora.</p>
                        </div>
                    </div>


                    <div className="col-sm-12 col-md-4 mb-4 mt-5 mt-lg-0 d-flex justify-content-center">
                        <div className="category-card raised">
                            <img className="img-fluid rounded" src="src/front/assets/img/61KR-pkP6ML._UF894,1000_QL80_.jpg" alt="quemadores" />
                            <h6 className="mt-2 fw-bold mt-lg-3">Quemadores</h6>
                            <p className="mt-lg-4">Diseños elegantes y funcionales para tus wax melts o aceites esenciales. Nuestros quemadores elevan la experiencia aromática con estilo.</p>
                        </div>
                    </div>

                    <div className="container mt-3 mt-lg-5">
                        <p className="text-muted small">Elige entre nuestras fragancias más vendidas y crea tu combinación ideal.</p>
                        <button className="btn btn-pink">Explorar →</button>
                    </div>

                </div>
            </div>
        </>
    )
}