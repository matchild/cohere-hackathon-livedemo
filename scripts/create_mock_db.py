from app.db import Base
from app.db.db import SessionLocal, engine
from app.db.schemas import DataframeFull, ValueLone, VariableFull
from app.db.services import register_full_dataframe

Base.metadata.create_all(bind=engine)
db = SessionLocal()

_ = register_full_dataframe(
    db,
    DataframeFull(
        name="CONTRACTS",
        description="This table contains all the information related to the active contracts the company has with its customers",
        variables=[
            VariableFull(
                name="amount",
                description="Contract amount in dollars",
                is_categorical=False,
                values=[],
            ),
            VariableFull(
                name="contract_type",
                description="Type of contract defining the commodity, market segment and branch of the company who issued the contract",
                is_categorical=True,
                values=[
                    ValueLone(
                        name="2A",
                        description="It is an energy contract issued by ABC branch for small business segment",
                    ),
                    ValueLone(
                        name="XB",
                        description="It is a waste contract issued by ABC branch for private homes",
                    ),
                    ValueLone(
                        name="3F",
                        description="It is a waste contract issued by WXY branch for large companies. These contracts were issued only from 2015 to 2018",
                    ),
                ],
            ),
            VariableFull(
                name="contract_name",
                description="Name given to the contract as shown in the finance database",
                is_categorical=False,
                values=[],
            ),
            VariableFull(
                name="is_active",
                description="Flag that keeps track of whether a contract is active or expired",
                is_categorical=True,
                values=[
                    ValueLone(
                        name="Active",
                        description="The expected end of the contract, calculated as the the date it was signed on plus the expected duration, has not yet been reached",
                    ),
                    ValueLone(
                        name="Expired",
                        description="The expected end date of the contact has been reached",
                    ),
                ],
            ),
        ],
    ),
)

_ = register_full_dataframe(
    db,
    DataframeFull(
        name="CUSTOMERS",
        description="This table contains all the information related to the customers",
        variables=[
            VariableFull(
                name="customer_name",
                description="Name of the customer",
                is_categorical=False,
                values=[],
            ),
            VariableFull(
                name="customer_tax_code",
                description="Tax code of the parent company",
                is_categorical=False,
                values=[],
            ),
            VariableFull(
                name="location",
                description="Geographical location of the client",
                is_categorical=True,
                values=[
                    ValueLone(
                        name="EU_West",
                        description="Countries served in Western Europe: Italy, Spain, Portugal",
                    ),
                    ValueLone(
                        name="EU_East",
                        description="Countries served in Eastern Europe: Poland, Netherlands, Finland",
                    ),
                    ValueLone(name="US", description="Any of the states in the US"),
                ],
            ),
        ],
    ),
)


db.close()
