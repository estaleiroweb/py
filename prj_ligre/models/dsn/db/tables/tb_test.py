from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, F
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from enum import Enum, auto


class Main():
    conn: str = 'evoice'
    """Connection of the database"""

    def __init__(self) -> None:
        super().__init__()
        self.xx = ''
        """test"""
    class fields:
        """Collection of the fields"""
        pass

    class keys:
        """Collection of the indexes"""
        pass

    class constraints:
        """Collection of the constraints"""
        pass

    class foreignKey:
        """Collection of the foreignKey"""
        pass

    class partitions:
        """Config of the partition"""
        pass

    class sql:
        """DDL, DML and DCL"""
        pass
    class data:
        """First data of table"""
        
    def test(self)->bool:
        """Test the table"""
        return True

class Table(Main):
    """comment"""

    conn = 'evoice'
    engine: str = 'MyISAM'
    name: str = 'tb_test'
    db: str = 'schema_db'
    collate: str = 'utf8_general_ci'
    row_format: str = 'FIXED'
    checksum: bool = False
    avg_row_length = None
    max_rows = None

    class fields:
        nome = models.CharField(max_length=100)
        "Nome do exemplo."

        descricao = models.TextField(blank=True, null=True)
        "Descrição detalhada."
        numero = models.IntegerField(default=0)
        "Valor numérico."

        decimal = models.DecimalField(max_digits=5, decimal_places=2)
        "Valor decimal."

        email = models.EmailField(blank=True, null=True)
        "Endereço de e-mail."

        url = models.URLField(blank=True, null=True)
        "URL do site."

        data = models.DateField(default=timezone.now)
        "Data de criação."

        tempo = models.TimeField(blank=True, null=True)
        "Horário."

        data_hora = models.DateTimeField(auto_now_add=True)
        "Data e hora de criação."

        booleano = models.BooleanField(default=False)
        "Valor booleano."

        arquivo = models.FileField(
            upload_to='arquivos/', blank=True, null=True)
        "Arquivo anexado."

        imagem = models.ImageField(upload_to='imagens/', blank=True, null=True)
        "Imagem anexada."

    class indexes:
        id = 0
        name = 1
        age = 2

    class sql:
        create = 'CREATE TABLE IF NOT EXISTS tb_test (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT)'
        drop = 'DROP TABLE IF EXISTS tb_test'
        insert = 'INSERT INTO tb_test (name, age) VALUES (%s, %s)'
        update = 'UPDATE tb_test SET name = %s, age = %s WHERE id = %s'
        delete = 'DELETE FROM tb_test WHERE id = %s'
        select = 'SELECT * FROM tb_test'
        select_id = 'SELECT * FROM tb_test WHERE id = %s'

    class data:
        insert = [
            ('John', 25),
            ('Peter', 28),
            ('Amy', 20),
            ('Hannah', 30),
            ('Michael', 35),
            ('Sandy', 40),
        ]
        update = [
            ('John', 26, 1),
            ('Peter', 29, 2),
            ('Amy', 21, 3),
            ('Hannah', 31, 4),
            ('Michael', 36, 5),
            ('Sandy', 41, 6),
        ]

    def test(self):
        self.create()
        self.insert()
        self.select()
        self.select_id()
        self.update()
        self.delete()
        self.drop()


print(Table.fields)


class ExemploModelo(models.Model):
    """
    Um modelo de exemplo para demonstrar vários tipos de campos, argumentos e métodos.
    """

    # Tipos de campos básicos
    nome = models.CharField(max_length=100, help_text="Nome do exemplo.")
    descricao = models.TextField(
        blank=True, null=True, help_text="Descrição detalhada.")
    numero = models.IntegerField(default=0, help_text="Valor numérico.")
    decimal = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Valor decimal.")
    email = models.EmailField(blank=True, null=True,
                              help_text="Endereço de e-mail.")
    url = models.URLField(blank=True, null=True, help_text="URL do site.")
    data = models.DateField(default=timezone.now, help_text="Data de criação.")
    tempo = models.TimeField(blank=True, null=True, help_text="Horário.")
    data_hora = models.DateTimeField(
        auto_now_add=True, help_text="Data e hora de criação.")
    booleano = models.BooleanField(default=False, help_text="Valor booleano.")
    arquivo = models.FileField(
        upload_to='arquivos/', blank=True, null=True, help_text="Arquivo anexado.")
    imagem = models.ImageField(
        upload_to='imagens/', blank=True, null=True, help_text="Imagem anexada.")

    # Relacionamentos
    relacionado = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                                    blank=True, help_text="Relacionamento com outro ExemploModelo.")
    muitos = models.ManyToManyField(
        'self', blank=True, help_text="Múltiplos relacionamentos com outros ExemploModelos.")

    # Escolhas
    ESCOLHAS_STATUS = (
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
        ('arquivado', 'Arquivado'),
    )
    status = models.CharField(max_length=20, choices=ESCOLHAS_STATUS,
                              default='rascunho', help_text="Status do exemplo.")

    # Métodos personalizados
    def __str__(self):
        return self.nome

    def salvar(self, *args, **kwargs):
        # Lógica personalizada ao salvar o modelo
        if self.numero < 0:
            self.numero = 0
        super().salvar(*args, **kwargs)

    @property
    def eh_publicado(self):
        # Propriedade para verificar se o exemplo está publicado
        return self.status == 'publicado'

    class Meta:
        # Metadados do modelo
        verbose_name = "Exemplo de Modelo"
        verbose_name_plural = "Exemplos de Modelos"
        ordering = ['-data_hora']
        unique_together = ['nome', 'data']

# Subclasses


class SubModelo(models.Model):
    """
    Um submodelo relacionado ao ExemploModelo.
    """
    exemplo = models.ForeignKey(ExemploModelo, on_delete=models.CASCADE)
    conteudo = models.TextField()

    def __str__(self):
        return self.conteudo


class SkillLevel(models.TextChoices):
    """Enumeration for skill levels"""
    BEGINNER = 'BEG', _('Beginner')
    INTERMEDIATE = 'INT', _('Intermediate')
    ADVANCED = 'ADV', _('Advanced')
    EXPERT = 'EXP', _('Expert')


class ContactType(models.TextChoices):
    """Contact method types"""
    PHONE = 'PHN', _('Phone')
    EMAIL = 'EML', _('Email')
    SOCIAL_MEDIA = 'SOC', _('Social Media')


class AuditMixin(models.Model):
    """Mixin for adding audit fields to models"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   related_name='%(class)s_created',
                                   null=True,
                                   blank=True)

    class Meta:
        abstract = True


class Address(models.Model):
    """Comprehensive address model with validation"""
    street = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3)],
        help_text="Full street address"
    )
    city = models.CharField(max_length=100)
    postal_code = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(4)]
    )
    country = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)

    def clean(self):
        """Custom validation method"""
        if len(self.postal_code) < 4:
            raise ValidationError("Postal code must be at least 4 characters")

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"


class Organization(AuditMixin):
    """Complex organization model with multiple relationships"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    founded_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Decimal field with precise monetary validation
    annual_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    # Many-to-many relationship with Address
    addresses = models.ManyToManyField(
        Address,
        related_name='organizations',
        blank=True
    )

    @classmethod
    def active_organizations(cls):
        """Custom class method to get active organizations"""
        return cls.objects.filter(is_active=True)

    def calculate_revenue_per_employee(self, employee_count):
        """Method to calculate revenue per employee"""
        if employee_count == 0:
            return Decimal('0.00')
        return self.annual_revenue / Decimal(str(employee_count))

    def __str__(self):
        return self.name


class Employee(AuditMixin):
    """Comprehensive employee model with multiple relationships and validations"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    # Relationship with Organization
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        related_name='employees'
    )

    # Choices and Enum integration
    skill_level = models.CharField(
        max_length=3,
        choices=SkillLevel.choices,
        default=SkillLevel.BEGINNER
    )

    # Contact information with type
    contact_type = models.CharField(
        max_length=3,
        choices=ContactType.choices,
        default=ContactType.EMAIL
    )
    contact_value = models.CharField(max_length=200)

    # Age with validation
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(18),
            MaxValueValidator(100)
        ]
    )

    # Generic foreign key example
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)

    def validate_contact(self):
        """Custom validation for contact information"""
        if self.contact_type == ContactType.EMAIL and '@' not in self.contact_value:
            raise ValidationError("Invalid email format")

    def get_full_name(self):
        """Custom method to get full name"""
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.get_full_name()

    class Meta:
        # Custom database table name
        db_table = 'hr_employees'
        # Compound unique constraint
        unique_together = ['user', 'organization']
        # Custom ordering
        ordering = ['user__last_name', 'user__first_name']

# Example of a complex query demonstration


def complex_employee_search(skill_level=None, min_age=None, organization=None):
    """
    Demonstrates complex querying capabilities
    """
    queryset = Employee.objects.all()

    # Chained filtering with Q objects
    if skill_level:
        queryset = queryset.filter(skill_level=skill_level)

    if min_age:
        queryset = queryset.filter(age__gte=min_age)

    if organization:
        queryset = queryset.filter(organization=organization)

    # Annotate and aggregate example
    return queryset.annotate(
        full_name=models.F('user__first_name') + ' ' +
        models.F('user__last_name')
    )
