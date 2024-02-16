from app.db import Base
from app.db.db import SessionLocal, engine
from app.db.schemas import DataframeFull, ValueLone, VariableFull
from app.db.services import register_full_dataframe

Base.metadata.create_all(bind=engine)

db = SessionLocal()
db.commit()


_ = register_full_dataframe(
    db,
    DataframeFull(
        name="Securities",
        description="This table contains information about each stock listed in NYSE and was last updated in September 2017 ",
        variables=[
            VariableFull(
                name="Ticker symbol",
                description="Unique abbreviation used to identify stocks",
                is_categorical=False,
                values=[],
            ),
            VariableFull(
                name="Security",
                description="Name of the stock",
                is_categorical=False,
                values=[],
            ),
            VariableFull(
                name="GICS Sector",
                description="This is the sector the company operates in. GICS stands for Global Industry Classification Standard.",
                is_categorical=True,
                values=[
                    ValueLone(
                        name="Financials",
                        description="Sector encompassing banks, insurance companies, and other financial institutions."
                    ),
                    ValueLone(
                        name="Health Care",
                        description="Sector focused on providing medical services and promoting wellness."
                    ),
                    ValueLone(
                        name="Industrials",
                        description="Sector encompassing manufacturing, construction, and infrastructure development industries."
                    ),
                    ValueLone(
                        name="Information Technology",
                        description="Sector involving the development, management, and use of technology for information processing and communication."
                    ),
                    ValueLone(
                        name="Materials",
                        description="Sector involved in the production and distribution of raw materials and commodities."
                    ),
                    ValueLone(
                        name="Real Estate",
                        description="Sector involving the buying, selling, and development of properties and land."
                    ),
                    ValueLone(
                        name="Utilities",
                        description="Sector responsible for providing essential services such as electricity, water, and gas to the public."
                    )
                ],
            ),
            VariableFull(
                name="Address of Headquarters",
                description="Physical location of the headquarter, expressed in the format City, State",
                is_categorical=False,
                values=[],
            ),
            VariableFull(
                name="Date first added",
                description="Date the listing was first added to the NYSE",
                is_categorical=False,
                values=[],
            ),
            VariableFull(
                name="CIK",
                description="Central Index Key. This is used to identify the company, person or entity.",
                is_categorical=False,
                values=[],
            )
        ],
    ),
)









db.close()
